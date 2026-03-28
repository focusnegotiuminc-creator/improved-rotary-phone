import Observation
import SwiftUI

struct HomeView: View {
    @Bindable var store: FocusAIAppStore

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                hero
                offerSection
                CompanyHighlightsView(companies: store.companies)
                workflowSection
            }
            .padding(20)
        }
        .background(FocusTheme.heroGradient.ignoresSafeArea())
        .task {
            if case .idle = store.loadState {
                await store.load()
            }
        }
    }

    private var hero: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text(store.portal?.siteName.uppercased() ?? "FOCUS AI")
                .font(.caption.weight(.semibold))
                .foregroundStyle(FocusTheme.gold)
                .tracking(1.4)

            Text("A customer-facing iPhone path into the same operating system powering the portal.")
                .font(.system(size: 34, weight: .bold, design: .serif))
                .foregroundStyle(FocusTheme.ink)

            Text("Browse live offers, enter the content library, submit intake, and let the assistant guide you toward the right next purchase path.")
                .font(.body)
                .foregroundStyle(FocusTheme.muted)

            Picker("Goal", selection: $store.selectedGoal) {
                Text("Start with the best entry offer").tag("Start with the best entry offer")
                Text("Get practical implementation assets").tag("Get practical implementation assets")
                Text("Build the operating system").tag("Build the operating system")
            }
            .pickerStyle(.segmented)

            if let offer = store.recommendedOffer {
                VStack(alignment: .leading, spacing: 6) {
                    Text("Recommended next step")
                        .font(.caption.weight(.semibold))
                        .foregroundStyle(FocusTheme.teal)
                    Text(offer.title)
                        .font(.headline)
                        .foregroundStyle(FocusTheme.ink)
                    Text(offer.summary)
                        .font(.subheadline)
                        .foregroundStyle(FocusTheme.muted)
                }
                .padding(16)
                .background(
                    RoundedRectangle(cornerRadius: 20, style: .continuous)
                        .fill(FocusTheme.panel.opacity(0.82))
                )
            }
        }
        .padding(22)
        .background(
            RoundedRectangle(cornerRadius: 28, style: .continuous)
                .fill(FocusTheme.panel.opacity(0.8))
        )
        .overlay(
            RoundedRectangle(cornerRadius: 28, style: .continuous)
                .stroke(FocusTheme.sky.opacity(0.16), lineWidth: 1)
        )
    }

    private var offerSection: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text("Live Offers")
                .font(.title2.weight(.semibold))
                .foregroundStyle(FocusTheme.ink)

            ForEach(Array(store.offers.enumerated()), id: \.element.id) { index, offer in
                OfferCardView(
                    offer: offer,
                    accent: index == 2 ? FocusTheme.ctaGradient : LinearGradient(colors: [FocusTheme.gold, FocusTheme.sky], startPoint: .leading, endPoint: .trailing)
                )
            }
        }
    }

    private var workflowSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Workflow Focus")
                .font(.title2.weight(.semibold))
                .foregroundStyle(FocusTheme.ink)

            ForEach(store.stages) { stage in
                VStack(alignment: .leading, spacing: 6) {
                    Text(stage.label)
                        .font(.headline)
                        .foregroundStyle(FocusTheme.ink)
                    Text(stage.description)
                        .font(.subheadline)
                        .foregroundStyle(FocusTheme.muted)
                }
                .padding(16)
                .background(
                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                        .fill(FocusTheme.panel.opacity(0.84))
                )
            }
        }
    }
}

