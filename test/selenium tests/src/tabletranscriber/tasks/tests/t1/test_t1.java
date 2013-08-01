package tabletranscriber.tasks.tests.t1;

import static org.junit.Assert.assertEquals;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriverBackedSelenium;
import org.openqa.selenium.firefox.FirefoxDriver;

import com.thoughtworks.selenium.Selenium;

public class test_t1 {
	private final int NUMBER_OF_TASKS_T1_BY_USER = 3;
	private Selenium selenium;

	@Before
	public void setUp() throws Exception {
		WebDriver driver = new FirefoxDriver();
		String baseUrl = "http://localhost";
		selenium = new WebDriverBackedSelenium(driver, baseUrl);
	}

	@Test
	public void testTest_t1_aaa() throws Exception {
		selenium.open("/pybossa/account/signin");
		selenium.type("email", "aaa@gmail.com");
		selenium.type("password", "aaa");
		selenium.click("xpath=/html/body/div[2]/form/div[4]/input");
		selenium.waitForPageToLoad("30000");
		
//		selenium.open("/pybossa/app/anuario1916pb_tt1/newtask");
		selenium.open("/pybossa/app/caracterizaoeten2001bras_tt1/newtask");
		
		for(int i = 0; i < NUMBER_OF_TASKS_T1_BY_USER; i++) {
			selenium.click("button_yes");
//			assertEquals("PyBossa · Application: Annuario Estatistico da Parahyba do Norte 1916 Seleção · Contribute", selenium.getTitle());
			assertEquals("PyBossa · Application: Caracterização e tendências da rede urbana do Brasil: configurações atuais e tendências da rede urbana Seleção · Contribute", selenium.getTitle());
		}
		
		selenium.close();
	}
	
	@Test
	public void testTest_t1_bbb() throws Exception {
		selenium.open("/pybossa/account/signin");
		selenium.type("email", "bbb@gmail.com");
		selenium.type("password", "bbb");
		selenium.click("xpath=/html/body/div[2]/form/div[4]/input");
		selenium.waitForPageToLoad("30000");
		
//		selenium.open("/pybossa/app/anuario1916pb_tt1/newtask");
		selenium.open("/pybossa/app/caracterizaoeten2001bras_tt1/newtask");
		
		for(int i = 0; i < NUMBER_OF_TASKS_T1_BY_USER; i++) {
			selenium.click("button_yes");
//			assertEquals("PyBossa · Application: Annuario Estatistico da Parahyba do Norte 1916 Seleção · Contribute", selenium.getTitle());
			assertEquals("PyBossa · Application: Caracterização e tendências da rede urbana do Brasil: configurações atuais e tendências da rede urbana Seleção · Contribute", selenium.getTitle());
		}
	}
	
	@Test
	public void testTest_t1_ccc() throws Exception {
		selenium.open("/pybossa/account/signin");
		selenium.type("email", "ccc@gmail.com");
		selenium.type("password", "ccc");
		selenium.click("xpath=/html/body/div[2]/form/div[4]/input");
		selenium.waitForPageToLoad("30000");
		
//		selenium.open("/pybossa/app/anuario1916pb_tt1/newtask");
		selenium.open("/pybossa/app/caracterizaoeten2001bras_tt1/newtask");
		
		for(int i = 0; i < NUMBER_OF_TASKS_T1_BY_USER; i++) {
			selenium.click("button_yes");
//			assertEquals("PyBossa · Application: Annuario Estatistico da Parahyba do Norte 1916 Seleção · Contribute", selenium.getTitle());
			assertEquals("PyBossa · Application: Caracterização e tendências da rede urbana do Brasil: configurações atuais e tendências da rede urbana Seleção · Contribute", selenium.getTitle());
		}
	}
	
	@After
	public void tearDown() throws Exception {
		selenium.stop();
	}
}
