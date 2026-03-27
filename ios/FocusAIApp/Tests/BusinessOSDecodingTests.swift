import XCTest
@testable import FocusAIApp

final class BusinessOSDecodingTests: XCTestCase {
    func testBundledBusinessOSPayloadDecodes() throws {
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        let json = """
        {
          "portal": {
            "brand": "Focus AI",
            "site_name": "Focus AI Business Operating System",
            "primary_contact": {
              "name": "Alexis Rogers",
              "phone": "2172576222",
              "role": "Primary routing contact"
            },
            "tracks": []
          },
          "offers": [
            {
              "id": "ebook-bundle",
              "title": "Focus AI eBook Bundle",
              "price_usd": 49,
              "summary": "Published eBooks",
              "cta_label": "Buy now",
              "checkout_url": "https://buy.stripe.com/bJe7sKh2B6ZQ8bP4II5os02"
            }
          ],
          "companies": [
            {
              "id": "focus-records",
              "name": "Focus Records LLC",
              "tagline": "Creative direction"
            }
          ],
          "workflow_stages": [],
          "app": {
            "app_name": "Focus AI",
            "features": [],
            "content_library_path": "/ebooks/index.html",
            "offers_path": "/products.html",
            "business_os_data_path": "/data/business_os.json"
          }
        }
        """
        let payload = try decoder.decode(BusinessOSPayload.self, from: XCTUnwrap(json.data(using: .utf8)))

        XCTAssertEqual(payload.offers.count, 1)
        XCTAssertEqual(payload.portal.brand, "Focus AI")
        XCTAssertEqual(payload.companies.count, 1)
    }
}
