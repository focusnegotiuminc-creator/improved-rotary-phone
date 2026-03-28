import Foundation
import Observation

@Observable
final class FocusAIAppStore {
    enum LoadState {
        case idle
        case loading
        case loaded
        case failed(String)
    }

    var loadState: LoadState = .idle
    var payload: BusinessOSPayload?
    var selectedGoal = "Start with the best entry offer"
    var intakeName = ""
    var intakeEmail = ""
    var intakeGoal = ""

    private let service: BusinessOSService

    init(service: BusinessOSService = BusinessOSService()) {
        self.service = service
    }

    @MainActor
    func load() async {
        loadState = .loading
        do {
            payload = try await service.fetchPayload()
            loadState = .loaded
        } catch {
            loadState = .failed(error.localizedDescription)
        }
    }

    var offers: [Offer] {
        payload?.offers ?? []
    }

    var companies: [Company] {
        payload?.companies ?? []
    }

    var stages: [WorkflowStage] {
        payload?.workflowStages ?? []
    }

    var portal: Portal? {
        payload?.portal
    }

    var recommendedOffer: Offer? {
        switch selectedGoal {
        case "Build the operating system":
            return offers.last
        case "Get practical implementation assets":
            return offers.dropFirst().first
        default:
            return offers.first
        }
    }
}

