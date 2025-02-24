using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using RazorLight;
using System.Threading.Tasks;

namespace VulnerableApp.Pages
{
    public class IndexModel : PageModel
    {
        [BindProperty]
        public string Description { get; set; }

        [BindProperty]
        public string CVSS { get; set; }

        [BindProperty]
        public string Impact { get; set; }

        [BindProperty]
        public string Remediation { get; set; }

        [BindProperty]
        public string References { get; set; }

        public string RenderedOutput { get; set; }

        public async Task OnPostAsync()
        {
            if (!string.IsNullOrEmpty(Description))
            {
                try
                {
                    var engine = new RazorLightEngineBuilder()
                        .UseEmbeddedResourcesProject(typeof(IndexModel))
                        .SetOperatingAssembly(typeof(IndexModel).Assembly)
                        .UseMemoryCachingProvider()
                        .Build();

                    RenderedOutput = await engine.CompileRenderStringAsync<object>("templateKey", Description, null);
                }
                catch (System.Exception ex)
                {
                    RenderedOutput = $"Error during template rendering: {ex.Message}";
                }
            }
        }
    }
}
