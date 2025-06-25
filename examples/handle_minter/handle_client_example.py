from handle_minter.handle_client import HandleClient

hc = HandleClient()

# Confirm that check_handle_exists with a known handle and a fake handle
print(hc.check_handle_exists("10113/10001"))
print(hc.check_handle_exists("fake_handle"))

#Check that check_landing_page_exists works with a known landing page and a fake one
print(hc.check_landing_page_exists("https://search.nal.usda.gov/permalink/01NAL_INST/27vehl/alma9916240546607426"))
print(hc.check_landing_page_exists("https://fake_landing_page"))

# Create a new handle, then confirm that the handle exists and the landing page exists
print(hc.create_handle("test-1111", "https://example.com/landing_page_1111"))
print(hc.check_handle_exists("10113/test-1111"))
print(hc.check_landing_page_exists("https://example.com/landing_page_1111"))