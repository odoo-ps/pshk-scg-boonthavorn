{
    "name": "Product Asset Sequence",  # TODO:
    # Explain the purpose of the module
    "summary": """
        Product Asset Sequence scaffold module
        """,
    "category": "",
    "version": "14.0.1.0.0",
    "author": "Odoo PS",
    "website": "http://www.odoo.com",
    "license": "OEEL-1",
    # TODO:
    # Check depends order uncomment if necessary
    "depends": [
         'account',
         'account_asset',
         'product',
    ],
    # TODO:
    # Check data order
    "data": [
        "data/sequences.xml",
        "views/account_asset.xml",
    ],
    # Only used to link to the analysis / Ps-tech store
    "task_id": [2516119],
}
