package main

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract provides functions for managing an Asset
type SmartContract struct {
	contractapi.Contract
}

// Transaction describes basic details of what being stored in the ledger
type Transaction struct {
	ID             string  `json:"ID"`
	Date           string  `json:"date"`
	FarmerID       string  `json:"farmerID"`
	ProductID      string  `json:"productID"`
	Quantity       float64 `json:"quantity"`
	Amount         float64 `json:"amount"`
	BlockchainHash string  `json:"blockchainHash"`
}

// InitLedger adds a base set of assets to the ledger
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	transactions := []Transaction{
		{ID: "TXN001", Date: "2024-01-01", FarmerID: "FMR001", ProductID: "PRD001", Quantity: 100, Amount: 50000, BlockchainHash: "init_hash_1"},
		{ID: "TXN002", Date: "2024-01-02", FarmerID: "FMR002", ProductID: "PRD002", Quantity: 200, Amount: 120000, BlockchainHash: "init_hash_2"},
	}

	for _, asset := range transactions {
		assetJSON, err := json.Marshal(asset)
		if err != nil {
			return err
		}

		err = ctx.GetStub().PutState(asset.ID, assetJSON)
		if err != nil {
			return fmt.Errorf("failed to put to world state. %v", err)
		}
	}

	return nil
}

// CreateTransaction issues a new asset to the world state with given details.
func (s *SmartContract) CreateTransaction(ctx contractapi.TransactionContextInterface, id string, date string, farmer string, product string, qty float64, amount float64) error {
	exists, err := s.TransactionExists(ctx, id)
	if err != nil {
		return err
	}
	if exists {
		return fmt.Errorf("the asset %s already exists", id)
	}

	timestamp := time.Now().String()
    // Simple mock hash generation
	hash := fmt.Sprintf("%s_%s_%s", id, farmer, timestamp)

	asset := Transaction{
		ID:             id,
		Date:           date,
		FarmerID:       farmer,
		ProductID:      product,
		Quantity:       qty,
		Amount:         amount,
		BlockchainHash: hash,
	}
	assetJSON, err := json.Marshal(asset)
	if err != nil {
		return err
	}

	return ctx.GetStub().PutState(id, assetJSON)
}

// ReadTransaction returns the asset stored in the world state with given id.
func (s *SmartContract) ReadTransaction(ctx contractapi.TransactionContextInterface, id string) (*Transaction, error) {
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if assetJSON == nil {
		return nil, fmt.Errorf("the asset %s does not exist", id)
	}

	var asset Transaction
	err = json.Unmarshal(assetJSON, &asset)
	if err != nil {
		return nil, err
	}

	return &asset, nil
}

// TransactionExists returns true when asset with given ID exists in world state
func (s *SmartContract) TransactionExists(ctx contractapi.TransactionContextInterface, id string) (bool, error) {
	assetJSON, err := ctx.GetStub().GetState(id)
	if err != nil {
		return false, fmt.Errorf("failed to read from world state: %v", err)
	}

	return assetJSON != nil, nil
}

// GetAllTransactions returns all assets found in world state
func (s *SmartContract) GetAllTransactions(ctx contractapi.TransactionContextInterface) ([]*Transaction, error) {
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var assets []*Transaction
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var asset Transaction
		err = json.Unmarshal(queryResponse.Value, &asset)
		if err != nil {
			return nil, err
		}
		assets = append(assets, &asset)
	}

	return assets, nil
}

func main() {
	chaincode, err := contractapi.NewChaincode(new(SmartContract))
	if err != nil {
		fmt.Printf("Error creating chaincode: %s", err.Error())
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting chaincode: %s", err.Error())
	}
}
