package drafts.leumivitality;

import java.util.List;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import drafts.leumivitality.e.Poller;
import drafts.leumivitality.e.YamlConf;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

@SpringBootApplication
@EnableSwagger2

public class M {

	
	

		public static void main(String[] args) {
		

			
			
			
			var c=SpringApplication.run(M.class, args);
			
			System.out.println(
					
					((List)(c.getBean(YamlConf.class).getConf().get("pus"))).get(0).getClass()
					
					
					);
		//	c.getBean(Poller.class).pollAll();
			
			
		}
}
