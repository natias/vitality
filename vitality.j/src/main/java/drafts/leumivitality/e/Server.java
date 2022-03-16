package drafts.leumivitality.e;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/")

public class Server {

	@Autowired
	Poller poller;
	
	@GetMapping("poll_all")
	public String pollAll() {
		
		return poller.pollAll();
		
	}
	
}
