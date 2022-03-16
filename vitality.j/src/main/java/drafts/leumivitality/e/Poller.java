package drafts.leumivitality.e;

import java.math.BigDecimal;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.ImmutableMap;
import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

@Component
public class Poller {

	@Autowired
	YamlConf conf;

	ExecutorService executorService = Executors.newCachedThreadPool();

	public String pollAll() {

		final RestTemplate restTemplate = new RestTemplate();

		/**
		 * resttemplate cofigure ssl: key stores passwords ssl auth
		 * 
		 */

		final List<Future<Map>> polls = new ArrayList();

		List<Map> pus = (List) conf.getConf().get("pus");

		pus.size(); // how many endpoints to scan

		pus.forEach(pu -> {

			
			
			System.out.println(pu.getClass());

			polls.add(executorService.submit(new Callable<Map>() {

				@Override
				public Map call() /* throws Exception */{
					
					long ll=System.currentTimeMillis();
					
					try {
						
					HttpEntity requestEntity = new HttpEntity("");
					Class responseType;

					long l = System.currentTimeMillis();
					
					
					String busp=(String)conf.getConf().get("base_url_server_part");
					
					String base_url_path=(String)conf.getConf().get("base_url_path");
					
					String url_specifier=(String)pu.get("url_specifier");
					
					
					String uri=busp+base_url_path+url_specifier;
					
					ResponseEntity<String> re;
						re = restTemplate.exchange(new URI(uri), HttpMethod.GET, requestEntity, String.class);
					
					l = System.currentTimeMillis() - l;

				;

					Map m = new HashMap<>();

					m.put("responseTime", l);

					m.put("status", re.getStatusCodeValue()==200 ? "Healthy":"Not Healthy"); 
					
					m.put("name", pu.get("name"));
					
					m.put(  "description", "OK, elapsed "+l+"ms");

					return m;
					
					} catch (RestClientException | URISyntaxException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}

					
					Map m = new HashMap<>();

					m.put("responseTime", (System.currentTimeMillis()-ll));

					m.put("status", "Not Healthy"); 
					
					m.put("name", pu.get("name"));
					
					m.put(  "description", "OK, elapsed "+(System.currentTimeMillis()-ll)+"ms");

					return m;

				}

			}));
		});

		Map<String, Object> result = new HashMap<String, Object>();

		final AtomicLong totlrt=new AtomicLong(0);
		
		final AtomicBoolean allHealthy=new AtomicBoolean(true);
		
		final List<Map> results=new ArrayList<Map>();;
		
		polls.forEach(p -> {

			try {

				var m = p.get();
				
				results.add(m);

				var e = (Long) m.get("responseTime");

				totlrt.addAndGet(e);
				
				var s = (String) m.get("status");
				
				allHealthy.set(allHealthy.get() && ( s.equalsIgnoreCase("Healthy")) );

			} catch (InterruptedException | ExecutionException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

		});

		result.put("applicationInfo", ImmutableMap.<String, Object>builder().put("applicationName", "ODS")
				.put("environment", "Productuion").put("Version", "1.0.0.9").build());

		//String status="";
		result.put("status", allHealthy.get()?"Healthy":"not Healthy");

		
		result.put("totalResponseTime", totlrt);

		
		result.put("results", results);

		return new Gson().toJson(result);

	}

	public static void main(String[] args) {

		Map<String, Object> l = new HashMap<String, Object>();

		l.put("a", 4);
		l.put("b", ImmutableMap.<String, Object>builder().put("applicationName", "O").build());
		l.put("c", ImmutableList.<Map<String, Object>>builder()
				.add(ImmutableMap.<String, Object>builder().put("status", "O").build()).build());

		System.out.println(new Gson().toJson(l));
	}

}
