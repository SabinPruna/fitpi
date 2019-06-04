using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(FP.Startup))]
namespace FP
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            ConfigureAuth(app);
        }
    }
}
