namespace chatter_app;

public class SignIn
{
    public string Username { get; set; }

    public string Password { get; set; } 

    public string Selector { get; set; }

    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);


}
