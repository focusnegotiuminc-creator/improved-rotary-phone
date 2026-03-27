import Observation
import SwiftUI

struct LibraryView: View {
    @Bindable var store: FocusAIAppStore

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                Text("Content Library")
                    .font(.largeTitle.weight(.bold))
                    .foregroundStyle(FocusTheme.ink)

                Text("Move from the app into the live library, public product pages, and the operating-system story without leaving the Focus AI brand context.")
                    .foregroundStyle(FocusTheme.muted)

                if let app = store.payload?.app,
                   let libraryURL = URL(string: "https://thefocuscorp.com\(app.contentLibraryPath)"),
                   let offersURL = URL(string: "https://thefocuscorp.com\(app.offersPath)") {
                    Link("Open the live eBook library", destination: libraryURL)
                        .focusLinkStyle()

                    Link("Open the live product ladder", destination: offersURL)
                        .focusLinkStyle()
                }

                VStack(alignment: .leading, spacing: 12) {
                    Text("Why this matters")
                        .font(.title3.weight(.semibold))
                        .foregroundStyle(FocusTheme.ink)
                    Text("The app and web experience share the same catalog, which keeps live offers, product sequencing, and messaging aligned.")
                        .foregroundStyle(FocusTheme.muted)
                }
                .padding(18)
                .background(
                    RoundedRectangle(cornerRadius: 24, style: .continuous)
                        .fill(FocusTheme.panel.opacity(0.86))
                )
            }
            .padding(20)
        }
        .background(FocusTheme.heroGradient.ignoresSafeArea())
    }
}

struct FocusLinkButtonStyle: ViewModifier {
    func body(content: Content) -> some View {
        content
            .font(.headline.weight(.bold))
            .foregroundStyle(.black)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 14)
            .background(FocusTheme.ctaGradient)
            .clipShape(RoundedRectangle(cornerRadius: 18, style: .continuous))
    }
}

extension View {
    func focusLinkStyle() -> some View {
        modifier(FocusLinkButtonStyle())
    }
}
