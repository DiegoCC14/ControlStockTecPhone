---
name: Horizon Enterprise
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#414754'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#727786'
  outline-variant: '#c1c6d7'
  surface-tint: '#005ac4'
  primary: '#0058c2'
  on-primary: '#ffffff'
  primary-container: '#0070f2'
  on-primary-container: '#fffeff'
  inverse-primary: '#aec6ff'
  secondary: '#49607d'
  on-secondary: '#ffffff'
  secondary-container: '#c4dcfe'
  on-secondary-container: '#4a617e'
  tertiary: '#4e5e71'
  on-tertiary: '#ffffff'
  tertiary-container: '#67778b'
  on-tertiary-container: '#fffeff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#aec6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004396'
  secondary-fixed: '#d2e4ff'
  secondary-fixed-dim: '#b1c8ea'
  on-secondary-fixed: '#021c36'
  on-secondary-fixed-variant: '#324864'
  tertiary-fixed: '#d3e4fb'
  tertiary-fixed-dim: '#b7c8de'
  on-tertiary-fixed: '#0c1d2d'
  on-tertiary-fixed-variant: '#38485a'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  display:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Hanken Grotesk
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  caption:
    fontFamily: Hanken Grotesk
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 14px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  container-max: 1440px
  gutter: 1rem
---

## Brand & Style

The design system is engineered for high-productivity enterprise environments, prioritizing clarity, trust, and functional efficiency. Drawing inspiration from modern industrial standards, the style balances a clean, "Horizon-inspired" aesthetic with the rigorous density required for complex data management.

The visual language is **Corporate Modern**, characterized by:
- **Functional Clarity:** Every element serves a purpose; decorative flair is minimized to reduce cognitive load.
- **Systematic Order:** Heavy reliance on a structured grid and consistent information hierarchy.
- **Professional Polish:** A refined palette of deep blues and neutral grays that evokes stability and institutional reliability.
- **High Information Density:** Optimized for expert users who need to view and manipulate large datasets without excessive scrolling.

## Colors

The color palette is anchored by **Deep Corporate Blues**. The primary blue (#0070f2) is used for action-oriented elements like primary buttons and active states, while the secondary deep navy (#0a243e) provides structural grounding in navigation shells and headers.

- **Backgrounds:** Use the neutral gray (#f5f6f7) for the application backdrop to provide subtle contrast against white surface containers.
- **Surfaces:** Cards, tables, and form containers must use pure white (#ffffff) to ensure maximum legibility.
- **Semantic Colors:** Status indicators follow standard enterprise conventions (Success Green, Error Red, Warning Orange) but are slightly desaturated to maintain a professional tone.
- **Borders:** Use a consistent light gray (#d9dadc) for hair-line dividers and input strokes to define structure without adding visual noise.

## Typography

This design system utilizes **Hanken Grotesk** for its exceptional legibility and neutral, professional character. It mimics the functional clarity of proprietary enterprise fonts while remaining modern.

- **Scale:** The system uses a tight scale to support high-density layouts. 14px is the standard body size for data-heavy views, while 16px is reserved for standard prose or marketing-adjacent content.
- **Hierarchy:** Use FontWeight 600 for sub-headers and labels to create clear visual separation without needing to increase font size.
- **Labels:** Small caps or slightly tracked-out labels (12px) should be used for table headers and form field captions to differentiate metadata from user data.

## Layout & Spacing

The layout philosophy follows a **Fixed-Fluid Hybrid** model. The main content area lives within a maximum width of 1440px for readability, but data tables and dashboards may expand to 100% width to accommodate large numbers of columns.

- **The 4px Grid:** All spacing (padding, margins, gutters) must be a multiple of 4px.
- **Density:** 
  - **Standard:** Use 16px (md) padding for containers.
  - **Compact:** Use 8px (sm) padding for data tables and toolbars to maximize information visibility.
- **Navigation Shell:** A fixed top-bar (64px height) and a collapsible side-navigation (240px width) provide the standard "Shell" structure.
- **Breakpoints:**
  - **Mobile:** < 600px (1 column, 16px margins)
  - **Tablet:** 601px - 1024px (Active side-rail, 24px margins)
  - **Desktop:** > 1025px (Full 12-column grid, 32px margins)

## Elevation & Depth

To maintain a clean, professional appearance, depth is communicated through **Tonal Layering** and **Low-Contrast Outlines** rather than heavy shadows.

- **Base Layer:** Background (#f5f6f7).
- **Surface Layer:** White (#ffffff) cards or sections with a 1px border (#d9dadc). No shadow is used for static containers.
- **Raised State:** Drop-downs, popovers, and modals use a very soft, ambient shadow (0px 4px 12px rgba(0,0,0,0.08)) to indicate they are temporary overlays.
- **Active State:** Elements like selected sidebar items or active tabs use a 2px vertical or horizontal primary blue (#0070f2) accent line rather than a depth change.

## Shapes

The design system adopts a **Soft** shape language. This prevents the UI from feeling too sharp and aggressive while maintaining a professional, structured feel.

- **Components:** Standard buttons, input fields, and cards use a 4px (0.25rem) corner radius.
- **Status Tags:** Use a slightly more rounded 8px (0.5rem) radius to differentiate them as discrete "pills."
- **Selection Indicators:** Checkboxes maintain a 2px radius to appear precise.

## Components

### Buttons
- **Primary:** Solid Blue (#0070f2) with white text. High-emphasis actions only.
- **Secondary:** White background with Blue border (#0070f2). Default for most actions.
- **Ghost:** No border, blue text. Used for toolbar actions or secondary navigation.

### Data Tables
- **Header:** Light gray background (#f5f6f7) with 12px bold labels. 1px bottom border.
- **Rows:** 40px height for compact density. Subtle hover state (#f0f2f5).
- **Cells:** 14px text. Align numeric data to the right.

### Input Fields
- **Design:** 32px height, white background, 1px gray border (#d9dadc).
- **Focus:** 2px solid primary blue border. Labels should be placed above the field in 12px bold.

### Cards
- **Structure:** White background, 1px border, 16px internal padding. 
- **Header:** Optional header section with a 1px bottom divider to separate title from content.

### Navigation Shell
- **Top Bar:** Deep navy (#0a243e) with white icons/text. Contains the logo, global search, and user profile.
- **Side Nav:** Vertical list of icons and labels. Selected state uses a light blue background tint and a 3px left-side primary blue border.