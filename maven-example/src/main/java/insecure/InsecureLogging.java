package insecure;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Demo of Software Composition Analysis with SonarQube
 * integration with dependency-check
 * See log4shell vulnerability detected on log4j dependency
 * in pom.xml file
 */
public class InsecureLogging 
{
	static final Logger logger = LogManager.getLogger(InsecureLogging.class);
	
	public static void main(String[] args) {
	
		InsecureLogging obj = new InsecureLogging();
		obj.runMe("This is a log");
		
	}
	
	private void runMe(String parameter){
		
		if (logger.isDebugEnabled()){
			logger.debug("This is debug : %s", parameter);
		}
		
		if(logger.isInfoEnabled()){
			logger.info("This is info : %s", parameter);
		}
		
		logger.warn("This is warn : %s", parameter);
		logger.error("This is error : %s", parameter);
		logger.fatal("This is fatal : %s", parameter);
		
	}
}
