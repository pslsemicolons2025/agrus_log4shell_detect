package insecure;

/**
 * This branch of the project makes no use of the vulnerable log4j lib
 */
public class InsecureLogging 
{
	
	public static void main(String[] args) {
	
		InsecureLogging obj = new InsecureLogging();
		obj.runMe("This is a log");
		
	}
	
	private void runMe(String parameter){

		System.out.println(parameter);
		
	}
}
