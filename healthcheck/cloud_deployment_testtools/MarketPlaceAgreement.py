from azure.mgmt.marketplaceordering import MarketplaceOrderingAgreements

def market_place_agreement(ref_arch_name, credentials, subscription_id):
    publisher = 'mathworks-inc'
    marketplace_ordering = MarketplaceOrderingAgreements(credentials, subscription_id)
    ref_arch_name == 'matlab-production-server-on-azure' :
    # Get sku details.
    offer1 = 'matlab-production-server-byol-windows'
    sku1 = 'matlab-production-server-byol-windows'
    offer2 = 'matlab-production-server-byol-linux'
    sku2 = 'matlab-production-server-byol-linux'
    create_agreements(marketplace_ordering, publisher, offer1, sku1)
    create_agreements(marketplace_ordering, publisher, offer2, sku2)
    print('Successful MPS agreement')

def create_agreements(marketplace_ordering, publisher, offer, plan) :
    term = marketplace_ordering.marketplace_agreements.get(publisher, offer, plan)
    term.accepted = True
    marketplace_ordering.marketplace_agreements.create(publisher, offer, plan, term)

    