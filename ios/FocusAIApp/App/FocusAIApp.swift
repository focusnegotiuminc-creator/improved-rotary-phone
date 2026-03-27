import SwiftUI

@main
struct FocusAIApp: App {
    @State private var store = FocusAIAppStore()

    var body: some Scene {
        WindowGroup {
            RootView(store: store)
                .preferredColorScheme(.dark)
        }
    }
}

