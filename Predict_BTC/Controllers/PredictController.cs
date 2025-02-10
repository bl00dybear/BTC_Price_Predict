using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace BTCPricePredictor.Controllers
{
    public class PredictController : Controller
    {
        private readonly HttpClient _httpClient;

        public PredictController(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        [HttpGet]
        public IActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Predict()
        {
            // Datele de intrare pentru model (un exemplu de secvență)
            var inputData = new
            {
                features = new double[][] {
                    new double[] { 12927.01, 13245.0, 12833.04, 13211.39, 298.22, 13060.99, 13187.07, 44.17, -133.85, -81.76, -52.09 }
                }
            };

            var jsonContent = new StringContent(JsonConvert.SerializeObject(inputData), Encoding.UTF8, "application/json");

            // Apelăm API-ul Python
            var response = await _httpClient.PostAsync("http://127.0.0.1:8000/predict/", jsonContent);
            var jsonResponse = await response.Content.ReadAsStringAsync();

            var result = JsonConvert.DeserializeObject<dynamic>(jsonResponse);
            ViewBag.Probability = result?.probability;

            return View("Index");
        }
    }
}