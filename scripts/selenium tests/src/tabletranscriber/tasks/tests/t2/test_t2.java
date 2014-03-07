package tabletranscriber.tasks.tests.t2;

import static org.junit.Assert.assertEquals;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriverBackedSelenium;
import org.openqa.selenium.firefox.FirefoxDriver;

import com.thoughtworks.selenium.Selenium;

public class test_t2 {
	private Selenium selenium;

	@Before
	public void setUp() throws Exception {
		WebDriver driver = new FirefoxDriver();
		String baseUrl = "http://localhost";
		selenium = new WebDriverBackedSelenium(driver, baseUrl);
	}
	
	@Test
	public void deleteTaskRunsType2() {
		//tabletranscriber.tasks.tests.setup.delete_tasks_runs.deleteTaskRunsType2.run();
	}

	@Test
	public void testTest_t2_aaa() throws Exception {
		selenium.open("/pybossa/account/signin");
		selenium.type("email", "aaa@gmail.com");
		selenium.type("password", "aaa");
		selenium.click("xpath=/html/body/div[2]/form/div[4]/input");
		selenium.waitForPageToLoad("30000");
		
		selenium.open("/pybossa/app/anuario1916pb_tt2/newtask");
		
		assertEquals(selenium.getTitle(), "PyBossa · Application: Annuario Estatistico da Parahyba do Norte 1916 Marcação · Contribute");

		selenium.mouseDownAt("xpath=/html/body/div[2]/div[7]/div/div", "100,214");
		//selenium.mouseOut("xpath=/html/body/div[2]/div[7]/div/div");
		//selenium.
		selenium.clickAt("xpath=/html/body/div[2]/div[7]/div/div", "451,284");
		selenium.click("xpath=/html/body/div[3]/a[2]");
		selenium.click("css=.btn-success");
		
//		selenium.clickAt("xpath=/html/body/div[2]/div[7]/div/div", "32,114");
//		selenium.mouseMoveAt("xpath=/html/body/div[2]/div[7]/div/div", "518,508");
//		selenium.click("xpath=/html/body/div[3]/a[2]");
//		selenium.click("css=.btn-success");
//		
//		selenium.clickAt("xpath=/html/body/div[2]/div[7]/div/div", "");
//		selenium.mouseMoveAt("xpath=/html/body/div[2]/div[7]/div/div", "");
//		selenium.click("xpath=/html/body/div[3]/a[2]");
//		selenium.click("css=.btn-success");
	}
	
//	@Test
//	public void testTest_t2_bbb() throws Exception {
//		selenium.open("/pybossa/account/signin");
//		selenium.type("email", "aaa@gmail.com");
//		selenium.type("password", "aaa");
//		selenium.click("xpath=/html/body/div[2]/form/div[4]/input");
//		selenium.waitForPageToLoad("30000");
//		
//		selenium.open("/pybossa/app/anuario1916pb_tt2/newtask");
////		selenium.click("xpath=/html/body/div[2]/section[2]/div/div/div/p[2]/a[2]");
//		
//		for(int i = 0; i < 3; i++) {
//			selenium.click("button_yes");
//			assertEquals("PyBossa · Application: Seleção de tabelas · Contribute", selenium.getTitle());
//		}
//	}

	@After
	public void tearDown() throws Exception {
		selenium.stop();
	}
}
