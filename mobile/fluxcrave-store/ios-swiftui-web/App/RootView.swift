import SwiftUI
import WebKit

struct RootView: View {
    private let appURL = URL(string: "https://www.fluxcrave.com/app/?source=ios-store")!
    private let orderURL = URL(string: "https://www.fluxcrave.com/online-ordering/")!
    private let directionsURL = URL(string: "https://www.google.com/maps/search/?api=1&query=3827%20Highway%20MM%2C%20Hannibal%2C%20MO%2063401")!
    private let callURL = URL(string: "tel:5737193159")!

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                WebView(url: appURL)
                Divider()
                HStack {
                    Link("Order", destination: orderURL)
                    Spacer()
                    Link("Directions", destination: directionsURL)
                    Spacer()
                    Link("Call", destination: callURL)
                    Spacer()
                    ShareLink(item: appURL) { Text("Share") }
                }
                .font(.headline)
                .padding(.horizontal, 18)
                .padding(.vertical, 12)
                .background(Color(red: 0.10, green: 0.07, blue: 0.05))
                .foregroundStyle(Color.orange)
            }
            .navigationTitle("Flux & Crave")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

struct WebView: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> WKWebView {
        let configuration = WKWebViewConfiguration()
        configuration.allowsInlineMediaPlayback = true
        let view = WKWebView(frame: .zero, configuration: configuration)
        view.allowsBackForwardNavigationGestures = true
        view.load(URLRequest(url: url))
        return view
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}
}
