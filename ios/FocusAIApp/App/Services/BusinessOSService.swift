import Foundation

struct BusinessOSService {
    let baseURL: URL

    init(baseURL: URL = URL(string: "https://thefocuscorp.com")!) {
        self.baseURL = baseURL
    }

    func fetchPayload() async throws -> BusinessOSPayload {
        let endpoint = baseURL.appending(path: "data/business_os.json")
        let request = URLRequest(url: endpoint)

        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            if let httpResponse = response as? HTTPURLResponse, 200 ..< 300 ~= httpResponse.statusCode {
                return try decoder.decode(BusinessOSPayload.self, from: data)
            }
        } catch {
            return try loadFallback()
        }

        return try loadFallback()
    }

    private func loadFallback() throws -> BusinessOSPayload {
        guard let url = Bundle.main.url(forResource: "business_os", withExtension: "json") else {
            throw URLError(.fileDoesNotExist)
        }
        let data = try Data(contentsOf: url)
        return try decoder.decode(BusinessOSPayload.self, from: data)
    }

    private var decoder: JSONDecoder {
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return decoder
    }
}

