import SwiftUI

struct RootView: View {
    let store: FocusAIAppStore

    var body: some View {
        TabView {
            HomeView(store: store)
                .tabItem {
                    Label("Home", systemImage: "sparkles")
                }

            LibraryView(store: store)
                .tabItem {
                    Label("Library", systemImage: "books.vertical")
                }

            IntakeFormView(store: store)
                .tabItem {
                    Label("Intake", systemImage: "text.badge.plus")
                }
        }
        .tint(FocusTheme.gold)
    }
}

