package tabletranscriber.tasks.tests.setup;

import java.util.concurrent.TimeUnit;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.firefox.FirefoxDriver;

public class initAnuariopb {
	private String baseUrl;
	private FirefoxDriver driver;

	@Before
	public void setUp() throws Exception {
		baseUrl = "http://localhost";
		driver = new FirefoxDriver();
		driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
	}

	@Test
	public void testInitAnuariopb() throws Exception {
		driver.get(baseUrl + "/mb/api/anuario1916pb/init");
//		assertEquals(selenium.getBodyText(), "True");
		driver.close();
	}

	@After
	public void tearDown() throws Exception {
		driver.quit();
	}
	
	@After
	public void selectPagesBooks() {
		selectBookPagesInDB.run();
	}
}
