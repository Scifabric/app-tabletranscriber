package tabletranscriber.tasks.tests.setup;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriverBackedSelenium;
import org.openqa.selenium.firefox.FirefoxDriver;

import com.thoughtworks.selenium.Selenium;

public class initCaracterizacao {
	private Selenium selenium;

	@Before
	public void setUp() throws Exception {
		WebDriver driver = new FirefoxDriver();
		String baseUrl = "http://localhost";
		selenium = new WebDriverBackedSelenium(driver, baseUrl);
	}

	@Test
	public void testInitCaracterizacao() throws Exception {
		selenium.open("/mb/api/caracterizaoeten2001bras/init");
		assertEquals(selenium.getBodyText(), "True");
		selenium.close();
	}

	@After
	public void tearDown() throws Exception {
		selenium.stop();
	}
}
