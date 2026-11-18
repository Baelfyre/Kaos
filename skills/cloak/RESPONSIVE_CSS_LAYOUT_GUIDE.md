# Responsive CSS Layout and Containment Guide

Use this guide to diagnose layout risk and define implementation-ready responsive requirements without writing production CSS.

## Layout model selection

- Use normal document flow as the default baseline.
- Use Flexbox for primarily one-dimensional distribution and alignment.
- Use Grid when rows and columns need coordinated two-dimensional placement.
- Nested layout models are valid when each level has a clear responsibility. Avoid layout mechanisms chosen only because they happen to make one screenshot align.
- Preserve semantic DOM order even when visual layout changes across breakpoints.

## CSS sizing units and scaling

CSS has more than five sizing units. Evaluate a unit by **what it is relative to**, the property it controls, and the actual layout context. These are starting recommendations, not a universal unit-to-property law; approved design tokens and measured behavior take precedence.

| Unit | What it measures | Appropriate use and caveat |
| --- | --- | --- |
| `px` | CSS reference pixels, not necessarily physical display pixels | Useful for fine borders, strokes, and deliberately fixed details. Browser zoom still changes their rendered appearance; fixed widths can overflow narrow containers, but `px` alone is not a defect. |
| `%` | A property-dependent percentage reference, commonly the containing block for width or a parent font size for `font-size` | Useful for fluid widths and containment. Percentages do not always resolve against the parent element's width; percentage heights can require a defined containing height. |
| `vw` | 1% of viewport width | Useful for intentionally viewport-relative dimensions, not automatically for all full-width sections. `100vw` can create horizontal overflow when scrollbars are present; container-width sizing is often safer. |
| `em` | The element's own computed font size for most properties; its **parent's** font size when used for `font-size` | Useful for component-local typography, padding, and proportions. Nested `font-size: 1.5em` multiplies across ancestors. |
| `rem` | The root element's computed font size | Prefer for readable type scales and font-related spacing that should scale consistently without compounded nested `em` font sizes. Preserve user-selected default font sizing when possible. |
| `fr` | A fraction of available grid-track space | Often preferable to fixed column widths for CSS Grid; available space and intrinsic minimums still determine whether content can shrink. |

**Font-size inheritance example:** with a 16px root, three nested levels each setting `font-size: 1.5em` produce `16 × 1.5³ = 54px` at the deepest level. A descendant setting `font-size: 1.5rem` computes to `24px` relative to that same root, regardless of nesting. This comparison assumes the root stays at 16px; changing its computed size changes `rem` results. An `em` used for a different property (for example padding) references that element's computed font size rather than multiplying a new font size by itself.

### Contextual unit-selection guidance

- **Typography:** start from `rem` or appropriate `em` values, not an inflexible fixed-pixel text scale. Avoid viewport-only font sizing. For fluid type, consider a bounded `clamp()` expression that retains a font-relative component.
- **Content widths and layout:** favor intrinsic sizing, `max-width`/`max-inline-size`, `%`, Grid `fr`, Flexbox, and container-responsive behavior based on the actual containment constraint. Never assume `width: 100%` by itself fixes min-content overflow or padding.
- **Viewport-sized sections:** use `vw` only when the viewport is genuinely the reference. Check scrollbar overflow, responsive containers, safe areas, and mobile dynamic viewports before recommending full-bleed or full-height dimensions.
- **Borders and small details:** `px` can be appropriate for consistent thin strokes; use established semantic tokens instead of introducing arbitrary hard-coded values.
- **Spacing:** honor project-approved spacing tokens and the optional soft 8-point rhythm. Token values may be expressed in `rem`, `em`, `px`, or other units as appropriate; an 8px rhythm is not a mandate to freeze text or layout dimensions.

### Responsive review checks

- Verify actual container and computed styles before blaming one unit for overflow. Check intrinsic minimum widths, padding, box sizing, unbroken strings, fixed children, Grid/Flex shrink constraints, and `100vw` scrollbar effects.
- Test narrow and intermediate viewports, browser zoom, increased default font size, text-only resizing where supported, longer localized text, and keyboard/focus visibility. Preserve reflow without page-level horizontal scrolling for ordinary application content; scoped scrolling can remain appropriate for wide data.
- Record whether a reported sizing problem is source-level risk or **rendered evidence**. State the selected unit, its reference, the reason, expected responsive behavior, and the smallest recommended fix. Ponytail implements CSS; Overseer owns validation gates.

## Consistency and anti-slop review

Review the **existing design system before suggesting a unit change**. A responsive UI can still look inconsistent when spacing, type scales, container rules, or component states vary without purpose.

1. **Source of truth:** inventory approved design tokens, typography hierarchy, container widths, spacing rhythm, and component variants. Reuse them first; do not introduce parallel `px`/`rem` scales, arbitrary one-off dimensions, or duplicate variants to fix isolated screenshots.
2. **Containment before cosmetic fixes:** trace the smallest element that causes overflow or reflow failure and its parent constraints. Do not recommend global `overflow-x: hidden`, clipping, extra breakpoints, forceful `!important`, or blanket `width: 100vw` as a substitute for diagnosing the cause.
3. **Consistent behavior across sizes:** comparable components must preserve spacing, typography, alignment, control height, interactive states, and reading order unless there is a justified responsive variant. Avoid exact-size cards or fixed-height text containers that cut off wrapped labels and error messages.
4. **Controlled adaptations:** prefer intrinsic wrap, flexible tracks, and content-driven breakpoints over device-specific pixel presets. Recommend a new breakpoint, token, or exception only when the existing system cannot support a demonstrated content requirement.
5. **No invented visual proof:** a lint rule or a source inspection can flag suspicious patterns, but cannot prove a layout is wrong or pixel-perfect. Report evidence, affected component and viewport, severity, suspected cause, smallest fix, and any accepted exception. Do not restyle a valid component to make it match an arbitrary aesthetic.
6. **Review acceptance:** target **zero unresolved confirmed critical/high-severity** layout, clipping, readability, focus, or navigation defects in the supported task flows. Verify ordinary content reflows without two-direction scrolling at **320 CSS px equivalent**, except content that legitimately needs two-dimensional layout (such as data tables); verify **200% text resize** without loss of content/function. Also exercise at least one intermediate viewport, zoom and long-content case. A static pass alone never establishes this target.

**Suggested handoff format:** affected screen/component; observed versus expected behavior; design token or CSS reference; applicable viewport/text condition; severity and evidence; smallest corrective constraint; Ponytail implementation owner; Overseer rendered verification. Reuse the existing Cloak output format rather than creating another report template.

## Intrinsic sizing literacy

Cloak should recognize common causes of unexpected overflow and compression.

- Long unbroken text, intrinsic media sizes, minimum content sizes, and nested flex/grid containers can force a layout wider than its container.
- A flex or grid child may need permission to shrink within its layout context. Diagnose the containing relationship before recommending arbitrary fixed widths.
- Grid tracks should account for content that must shrink or wrap. Avoid layouts whose minimum track size silently preserves desktop width on narrow screens.
- Media should respect its containing region and preserve meaningful aspect ratio unless product requirements explicitly call for cropping.

## Overflow and clipping

Treat overflow as a user-visible behavior decision, not merely a cosmetic property.

- Horizontal scrolling on the entire page is usually a containment defect for ordinary application layouts.
- Local horizontal scrolling can be appropriate for wide data tables, timelines, code, or other content whose two-dimensional relationship must remain intact.
- Clipping must not hide focus indicators, validation messages, menus, tooltips, or actionable content.
- Text truncation needs an evidence-backed reason. Critical labels, values, and error messages should remain perceivable without relying on hover-only disclosure.
- Inspect ancestor overflow, positioning, transforms, and stacking contexts when popovers or focus rings appear cut off.

## Breakpoints and reflow

- Define breakpoints from content pressure and task preservation, not device-name folklore alone.
- Preserve primary task order when columns collapse or navigation changes form.
- Check the narrowest supported viewport, intermediate widths, landscape orientation, text enlargement, browser zoom, and long localized content.
- A responsive design is not complete if a control is merely moved off-screen or hidden without an equivalent accessible path.
- If container queries are already part of the project architecture, review component behavior against its actual container rather than assuming the full viewport controls every layout decision.

## Fixed, sticky, and overlay UI

- Fixed or sticky headers, footers, action bars, and cookie/consent surfaces must not cover focused controls or required content.
- Account for mobile safe areas and on-screen keyboards when they can obscure form actions.
- Verify nested scrolling does not trap keyboard or touch users inside an unexpected region.
- Overlay layering should preserve one clear active interaction surface and predictable dismissal behavior.

## Data-heavy surfaces

For tables, dashboards, grids, and charts:

- Preserve labels, units, legends, and critical comparisons at narrow widths.
- Choose deliberately among column prioritization, wrapping, stacked summaries, local horizontal scroll, or alternate detail views.
- Do not convert tabular relationships into visually convenient cards if that destroys comparisons users need to make.
- Provide an accessible summary or data alternative when a chart alone cannot communicate the decision-relevant information.

## Motion and responsive state

- Layout changes should not create unnecessary motion or spatial disorientation.
- Respect reduced-motion preferences when transitions or animated reflow are part of the experience.
- Loading skeletons, drawers, accordions, and responsive navigation must preserve focus and state when viewport conditions change.

## Review evidence

A static source review may return `STATIC_UI_RISK_LOW`, `STATIC_UI_RISK_DETECTED`, or `STATIC_UI_RESULT_INCONCLUSIVE` according to Cloak's existing contract. Rendered correctness still requires current visual evidence.

## Primary references

- CSS Grid Layout: https://www.w3.org/TR/css-grid-2/
- CSS Flexible Box Layout: https://www.w3.org/TR/css-flexbox-1/
- CSS Overflow: https://www.w3.org/TR/css-overflow-3/
- MDN CSS values and units: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Values_and_units
- MDN responsive design: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design
- Google web.dev sizing units: https://web.dev/learn/css/sizing/
- WCAG 2.2 reflow and focus requirements: https://www.w3.org/TR/WCAG22/