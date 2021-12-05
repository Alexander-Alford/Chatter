using Microsoft.AspNetCore.Mvc;

namespace chatter_app.Controllers;

[ApiController]
[Route("api")]

public class SignInController : Controller
{

    private readonly ILogger<SignInController> _logger;

    public SignInController(ILogger<SignInController> logger)
    {
        _logger = logger;
    }


    [HttpPost]
    public IActionResult Index([FromBody] SignIn data)
    {
        return Json(data);
    }

    [HttpGet]
    public string Get()
    {
        return "Hello World";
    }


}
