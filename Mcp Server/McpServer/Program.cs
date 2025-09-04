var builder = WebApplication.CreateBuilder(args);

builder.Services
    .AddMcpServer()
    .WithHttpTransport()
    .WithResourcesFromAssembly()
    .WithToolsFromAssembly();


builder.Services.AddHttpClient("Faiss", options =>
{
    options.BaseAddress = new Uri("http://127.0.0.1:8000");
});

var app = builder.Build();

app.MapMcp();

app.Run();