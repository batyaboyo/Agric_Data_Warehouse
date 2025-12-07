-- ============================================================================
-- View: Supply Chain Sankey Flow
-- Agricultural Supply Chain Data Warehouse
-- ============================================================================
-- Purpose: Transform transactional data into Source-Target pairs for Sankey Diagram
-- Schema: dw
-- ============================================================================

CREATE OR REPLACE VIEW dw.view_supply_chain_sankey AS
WITH flow_data AS (
    -- Flow 1: Farmer -> Product
    SELECT 
        f.full_name || ' (Farmer)' as source_node,
        p.product_name || ' (Product)' as target_node,
        SUM(t.quantity_kg) as total_quantity,
        SUM(t.total_amount) as total_value,
        COUNT(t.transaction_id) as transaction_count,
        '1. Production' as flow_stage,
        1 as step_order
    FROM dw.fact_transaction t
    JOIN dw.dim_farmer f ON t.farmer_key = f.farmer_key
    JOIN dw.dim_product p ON t.product_key = p.product_key
    WHERE t.blockchain_hash IS NOT NULL -- Only trace verified transactions
    GROUP BY f.full_name, p.product_name

    UNION ALL

    -- Flow 2: Product -> Market
    SELECT 
        p.product_name || ' (Product)' as source_node,
        m.market_name || ' (Market)' as target_node,
        SUM(t.quantity_kg) as total_quantity,
        SUM(t.total_amount) as total_value,
        COUNT(t.transaction_id) as transaction_count,
        '2. Distribution' as flow_stage,
        2 as step_order
    FROM dw.fact_transaction t
    JOIN dw.dim_product p ON t.product_key = p.product_key
    JOIN dw.dim_market m ON t.market_key = m.market_key
    WHERE t.blockchain_hash IS NOT NULL
    GROUP BY p.product_name, m.market_name

    UNION ALL

    -- Flow 3: Market -> Buyer
    SELECT 
        m.market_name || ' (Market)' as source_node,
        b.buyer_name || ' (Buyer)' as target_node,
        SUM(t.quantity_kg) as total_quantity,
        SUM(t.total_amount) as total_value,
        COUNT(t.transaction_id) as transaction_count,
        '3. Retail' as flow_stage,
        3 as step_order
    FROM dw.fact_transaction t
    JOIN dw.dim_market m ON t.market_key = m.market_key
    JOIN dw.dim_buyer b ON t.buyer_key = b.buyer_key
    WHERE t.blockchain_hash IS NOT NULL
    GROUP BY m.market_name, b.buyer_name
)
SELECT 
    source_node,
    target_node,
    total_quantity,
    total_value,
    transaction_count,
    flow_stage,
    step_order
FROM flow_data;

COMMENT ON VIEW dw.view_supply_chain_sankey IS 'Sankey diagram compatible view showing flow from Farmer -> Product -> Market -> Buyer for verified transactions';
