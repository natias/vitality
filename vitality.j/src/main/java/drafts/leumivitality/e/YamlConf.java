package drafts.leumivitality.e;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.Map;

import javax.annotation.PostConstruct;

import org.springframework.stereotype.Component;
import org.yaml.snakeyaml.Yaml;

import lombok.extern.slf4j.Slf4j;

@Component
@Slf4j
public class YamlConf {

	private static final String HOME_NATI_DEV_LEUMI_VITALITY_VITALITY_CONF_YAML = "/home/nati/dev/leumi/vitality/vitality_conf.yaml";
	Map conf;

	Long lmt = -1l;

	@PostConstruct
	public void init() {
		var v=getConf() ;
		
		log.info("vvvvvvvvvvvvvvvvv {}",v);
		
	}

	private long getLMT() throws IOException {
		Path file = Paths.get(HOME_NATI_DEV_LEUMI_VITALITY_VITALITY_CONF_YAML);

		BasicFileAttributes attr = Files.readAttributes(file, BasicFileAttributes.class);

		return attr.lastModifiedTime().toMillis();
	}

	private void refreshConf()/* throws IOException */{

		Yaml yaml = new Yaml();

		try {
			long clmt =

					getLMT();

			if (clmt > lmt) {
				lmt=clmt;

				conf = yaml.load(new FileInputStream(HOME_NATI_DEV_LEUMI_VITALITY_VITALITY_CONF_YAML));
			}
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public Map getConf() {
		
		refreshConf();
		
		return conf;
	}

	public static void main(String[] args) throws FileNotFoundException {
		// TODO Auto-generated method stub

		Yaml yaml = new Yaml();

		var o = yaml.load(new FileInputStream(HOME_NATI_DEV_LEUMI_VITALITY_VITALITY_CONF_YAML));

		System.out.println(o.getClass());

		System.out.println(((Map) o).get("pus").getClass());

	}

//	String loadConf() {
//		
//	}

}
