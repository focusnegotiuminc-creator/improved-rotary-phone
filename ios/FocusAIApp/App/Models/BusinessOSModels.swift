import Foundation

struct BusinessOSPayload: Codable {
    let portal: Portal
    let offers: [Offer]
    let companies: [Company]
    let workflowStages: [WorkflowStage]
    let app: AppConfig
}

struct Portal: Codable {
    let brand: String
    let siteName: String
    let primaryContact: PrimaryContact
    let tracks: [Track]
}

struct PrimaryContact: Codable {
    let name: String
    let phone: String
    let role: String
}

struct Track: Codable, Identifiable {
    let id: String
    let title: String
    let summary: String
}

struct Offer: Codable, Identifiable {
    let id: String
    let title: String
    let priceUsd: Int
    let summary: String
    let ctaLabel: String
    let checkoutURL: URL
}

struct Company: Codable, Identifiable {
    let id: String
    let name: String
    let tagline: String
}

struct WorkflowStage: Codable, Identifiable {
    let id: String
    let label: String
    let description: String
}

struct AppConfig: Codable {
    let appName: String
    let features: [String]
    let contentLibraryPath: String
    let offersPath: String
    let businessOSDataPath: String
}

