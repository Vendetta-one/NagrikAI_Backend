<!-- LOVABLE:BEGIN -->
> [!IMPORTANT]
> This project is connected to [Lovable](https://lovable.dev). Avoid rewriting
> published git history — force pushing, or rebasing/amending/squashing commits
> that are already pushed — as it rewrites history on Lovable's side and the
> user will likely lose their project history.
>
> Commits you push to the connected branch sync back to Lovable and show up in
> the editor, so keep the branch in a working state.
<!-- LOVABLE:END -->

## Application architecture
- Keep page-specific content in leaf routes and the shared GovTech navigation in AppShell around the root Outlet, so every screen has consistent navigation and unique metadata.
- Keep the research demonstration deterministic and explicitly labeled; use DemoProvider with browser-session storage for non-sensitive simulated complaints, not as a production grievance database.
- Keep color, typography, layout and animation styling in the global semantic design system so all grievance pages share the same visual language.
