using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
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
            try
            {
                // Apelăm API-ul Python (nu mai trimitem `null`, deoarece API-ul ia singur datele)
                var response = await _httpClient.PostAsync("http://127.0.0.1:8000/predict/", null);

                // Verificăm dacă API-ul a răspuns cu succes
                if (!response.IsSuccessStatusCode)
                {
                    ViewBag.Error = "Eroare la API-ul de predicție!";
                    return View("Index");
                }

                // Extragem și interpretăm răspunsul
                var jsonResponse = await response.Content.ReadAsStringAsync();
                var result = JsonConvert.DeserializeObject<dynamic>(jsonResponse);

                if (result?.probability != null)
                {
                    ViewBag.Probability = (double)result.probability;
                }
                else
                {
                    ViewBag.Error = "API-ul a returnat un rezultat null.";
                }
            }
            catch (HttpRequestException)
            {
                ViewBag.Error = "Nu se poate contacta API-ul Python.";
            }
            catch (JsonException)
            {
                ViewBag.Error = "Eroare la procesarea răspunsului API.";
            }

            return View("Index");
        }
    }
}