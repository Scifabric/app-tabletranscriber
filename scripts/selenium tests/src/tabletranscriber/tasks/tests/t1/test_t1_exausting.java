package tabletranscriber.tasks.tests.t1;

import static org.junit.Assert.assertEquals;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriverBackedSelenium;
import org.openqa.selenium.firefox.FirefoxDriver;

import com.thoughtworks.selenium.Selenium;

public class test_t1_exausting {
	private Selenium selenium;

	@Before
	public void setUp() throws Exception {
		WebDriver driver = new FirefoxDriver();
		String baseUrl = "http://localhost";
		selenium = new WebDriverBackedSelenium(driver, baseUrl);
	}

	@Test
	public void testTest_t1_guilherme() throws Exception {
		selenium.open("/pybossa/account/signin");
		selenium.type("email", "ccc@gmail.com");
		selenium.type("password", "ccc");
		selenium.click("xpath=/html/body/div[2]/form/div[4]/input");
		selenium.waitForPageToLoad("30000");
		selenium.click("xpath=/html/body/div[2]/section[2]/div/div[2]/div/p[2]/a[2]");
		assertEquals("PyBossa · Application: Marcação de tabelas · Contribute", selenium.getTitle());
		selenium.click("xpath=//*[@id=\"button\"]");
		selenium.waitForPageToLoad("30000");
		selenium.setCursorPosition("image-annotate-view", "22.5 , 141");
		selenium.mouseMoveAt("image-anotate-view", "300 , 400");
		selenium.click("image-annotate-edit-ok");
	}
	
	@Test
	public void testTest_t1_aaa() throws Exception {
		selenium.open("/pybossa/account/signin");
		selenium.type("email", "aaa@gmail.com");
		selenium.type("password", "aaa");
		selenium.click("xpath=/html/body/div[2]/form/div[4]/input");
		selenium.waitForPageToLoad("30000");
		selenium.click("xpath=/html/body/div[2]/section[2]/div/div[2]/div/p[2]/a[2]");
		assertEquals("PyBossa · Application: Marcação de tabelas · Contribute", selenium.getTitle());
		selenium.click("xpath=//*[@id=\"button\"]");
		selenium.waitForPageToLoad("30000");
		selenium.setCursorPosition("image-annotate-view", "22.5 , 141");
		selenium.mouseMoveAt("image-anotate-view", "300 , 400");
		selenium.click("image-annotate-edit-ok");
	}

	@After
	public void tearDown() throws Exception {
		selenium.stop();
	}
}
