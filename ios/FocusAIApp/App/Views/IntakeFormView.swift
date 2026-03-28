import Observation
import SwiftUI

struct IntakeFormView: View {
    @Bindable var store: FocusAIAppStore

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 18) {
                Text("Service Intake")
                    .font(.largeTitle.weight(.bold))
                    .foregroundStyle(FocusTheme.ink)

                Text("Capture the visitor’s focus, then route them into booking or the right product path.")
                    .foregroundStyle(FocusTheme.muted)

                Group {
                    TextField("Name", text: $store.intakeName)
                    TextField("Email", text: $store.intakeEmail)
                        .textInputAutocapitalization(.never)
                        .keyboardType(.emailAddress)
                    TextField("Goal", text: $store.intakeGoal, axis: .vertical)
                        .lineLimit(3...5)
                }
                .padding(14)
                .background(
                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                        .fill(FocusTheme.panel.opacity(0.88))
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 18, style: .continuous)
                        .stroke(FocusTheme.sky.opacity(0.18), lineWidth: 1)
                )
                .foregroundStyle(FocusTheme.ink)

                if let contact = store.portal?.primaryContact,
                   let bookingURL = URL(string: "tel:\(contact.phone)") {
                    Link("Call \(contact.name) at \(contact.phone)", destination: bookingURL)
                        .focusLinkStyle()
                }

                Text("This app scaffold keeps high-risk actions in readiness-only mode. Intake and routing can be automated, but legal, payroll, and banking execution still require an approved operator.")
                    .font(.footnote)
                    .foregroundStyle(FocusTheme.muted)
            }
            .padding(20)
        }
        .background(FocusTheme.heroGradient.ignoresSafeArea())
    }
}
