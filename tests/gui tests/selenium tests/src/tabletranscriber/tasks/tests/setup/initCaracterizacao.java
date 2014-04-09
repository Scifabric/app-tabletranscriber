package tabletranscriber.tasks.tests.setup;

import static org.junit.Assert.*;

import java.util.concurrent.TimeUnit;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.firefox.FirefoxDriver;

public class initCaracterizacao {
	private String baseUrl = "http://localhost";
	private FirefoxDriver driver;

	@Before
	public void setUp() throws Exception {
		driver = new FirefoxDriver();
		driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
	}

	@Test
	public void testInitCaracterizacao() throws Exception {
		driver.get(baseUrl + "/mb/api/caracterizaoeten2001bras/init");
		assertEquals(driver.findElement(By.xpath("/html/body")).getText(), "True");
		driver.close();
	}

	@After
	public void tearDown() throws Exception {
		driver.quit();
	}
	
//	@After
//	public void selectBookPages() {
//		selectBookPagesInDB.run();
//	}
}
