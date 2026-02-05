using System;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace trigger
{
    class Program
    {
        
        static async Task Main(string[] args)
        {
            using (var client = new HttpClient())
            {
                var values = new Dictionary<string, string>
                {
                };

                var content = new FormUrlEncodedContent(values);
                var response = await client.PostAsync("http://192.168.0.120/cgi-bin/alarm.cgi?userName=admin&password=admin&action=manualControl&alarmOutID=1&controlFlag=1", content);
                var responseString = await response.Content.ReadAsStringAsync();
                Console.WriteLine(responseString);
            }
        }
    }
}
