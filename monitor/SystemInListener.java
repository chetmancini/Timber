import java.util.Scanner;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class SystemInListener implements Runnable {
	private final ExecutorService executor = Executors.newCachedThreadPool();
	
	private Scanner scanner = new Scanner(System.in);
	
	public SystemInListener(){
		
	}
	
	@Override
	public void run() {
		boolean running = true;
		while (running) {
			String inputstr = scanner.next();
			
		}
	}

}
