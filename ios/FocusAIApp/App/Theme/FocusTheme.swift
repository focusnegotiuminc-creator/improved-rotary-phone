import SwiftUI

enum FocusTheme {
    static let background = Color(red: 5 / 255, green: 8 / 255, blue: 18 / 255)
    static let panel = Color(red: 14 / 255, green: 23 / 255, blue: 48 / 255)
    static let ink = Color(red: 246 / 255, green: 248 / 255, blue: 1.0)
    static let muted = Color(red: 194 / 255, green: 204 / 255, blue: 229 / 255)
    static let gold = Color(red: 242 / 255, green: 201 / 255, blue: 109 / 255)
    static let teal = Color(red: 62 / 255, green: 228 / 255, blue: 214 / 255)
    static let sky = Color(red: 124 / 255, green: 200 / 255, blue: 1.0)
    static let ember = Color(red: 255 / 255, green: 155 / 255, blue: 104 / 255)

    static let heroGradient = LinearGradient(
        colors: [background, Color(red: 10 / 255, green: 19 / 255, blue: 41 / 255), Color(red: 8 / 255, green: 23 / 255, blue: 46 / 255)],
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )

    static let ctaGradient = LinearGradient(
        colors: [gold, Color(red: 1.0, green: 217 / 255, blue: 143 / 255), ember],
        startPoint: .leading,
        endPoint: .trailing
    )
}

