import SwiftUI

struct CompanyHighlightsView: View {
    let companies: [Company]

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Operating Companies")
                .font(.title2.weight(.semibold))
                .foregroundStyle(FocusTheme.ink)

            ForEach(companies) { company in
                VStack(alignment: .leading, spacing: 6) {
                    Text(company.name)
                        .font(.headline)
                        .foregroundStyle(FocusTheme.ink)
                    Text(company.tagline)
                        .font(.subheadline)
                        .foregroundStyle(FocusTheme.muted)
                }
                .padding(16)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(
                    RoundedRectangle(cornerRadius: 20, style: .continuous)
                        .fill(FocusTheme.panel.opacity(0.85))
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 20, style: .continuous)
                        .stroke(FocusTheme.sky.opacity(0.16), lineWidth: 1)
                )
            }
        }
    }
}

