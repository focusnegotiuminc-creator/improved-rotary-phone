import SwiftUI

struct OfferCardView: View {
    let offer: Offer
    let accent: LinearGradient

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(offer.title.uppercased())
                .font(.caption.weight(.semibold))
                .foregroundStyle(FocusTheme.gold)
                .tracking(1.5)

            Text(offer.title)
                .font(.title3.weight(.semibold))
                .foregroundStyle(FocusTheme.ink)

            Text(offer.summary)
                .font(.subheadline)
                .foregroundStyle(FocusTheme.muted)

            Text("$\(offer.priceUsd) USD")
                .font(.headline.weight(.bold))
                .foregroundStyle(FocusTheme.gold)

            Link(destination: offer.checkoutURL) {
                Text(offer.ctaLabel)
                    .font(.subheadline.weight(.bold))
                    .foregroundStyle(.black)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 12)
                    .background(accent)
                    .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
            }
        }
        .padding(18)
        .background(
            RoundedRectangle(cornerRadius: 24, style: .continuous)
                .fill(FocusTheme.panel.opacity(0.92))
        )
        .overlay(
            RoundedRectangle(cornerRadius: 24, style: .continuous)
                .stroke(FocusTheme.sky.opacity(0.18), lineWidth: 1)
        )
    }
}

