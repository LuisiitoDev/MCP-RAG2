using System.ComponentModel;
using ModelContextProtocol.Server;

namespace McpServer.Resources;

[McpServerToolType]
public class FaissResource(IHttpClientFactory factory)
{
    [McpServerTool]
    [Description("Devuelve documentos de referencia sobre facturas para ser usados como contexto en respuestas de facturación.")]
    public async Task<string> Invoice_Context_Reference(string query)
    {
        using var client = factory.CreateClient("Faiss");
        var response = await client.GetAsync($"/search?q={query}");
        return await response.Content.ReadAsStringAsync();
    }
}