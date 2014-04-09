package tabletranscriber.tasks.tests.t2;

import static org.junit.Assert.fail;

import java.util.concurrent.TimeUnit;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxProfile;
import org.openqa.selenium.interactions.Action;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import tabletranscriber.tasks.tests.util.Util;

public class test_t2 {
	private final int NUMBER_OF_TASK_RUNS_T2_BY_USER = 5;

	private StringBuffer verificationErrors = new StringBuffer();
	private WebDriver driver;
	private FirefoxProfile profile;
	private String baseUrl = "http://localhost";

	@Before
	public void setUp() throws Exception {
		profile = new FirefoxProfile();
		profile.setEnableNativeEvents(true);
		driver = new FirefoxDriver(profile);
		driver.manage().window().setSize(new Dimension(1200, 700));
		driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
	}

	@Test
	public void testTest_t2_aaa() throws Exception {
		Util.login(driver, baseUrl, "aaa@gmail.com", "aaa");

		driver.get(baseUrl
				+ "/pybossa/app/caracterizaoeten2001bras_tt2/newtask");

		
		for (int i = 0; i < NUMBER_OF_TASK_RUNS_T2_BY_USER; i++) {
			WebDriverWait wait = new WebDriverWait(driver, 60000);
			wait.until(ExpectedConditions.visibilityOf(driver.findElement(By.xpath("//*[@id='TTImage']/div/div[1]"))));
			
			WebElement image = driver.findElement(By
					.xpath("//*[@id='TTImage']/div/div[1]"));

			Actions builder = new Actions(driver);
			Action makeAnottation = builder.moveToElement(image).clickAndHold()
					.moveByOffset(100, 200).click().build();
			makeAnottation.perform();

			wait.until(ExpectedConditions.visibilityOfElementLocated(By
					.xpath("//*[@id='image-annotate-edit-form']/a[1]")));

			driver.findElement(
					By.xpath("//*[@id='image-annotate-edit-form']/a[1]"))
					.click();

			driver.findElement(By.xpath("//*[@id='button']")).click();

		}
	}

	@Test
	public void testTest_t2_bbb() throws Exception {
		Util.login(driver, baseUrl, "bbb@gmail.com", "bbb");

		driver.get(baseUrl
				+ "/pybossa/app/caracterizaoeten2001bras_tt2/newtask");

		
		for (int i = 0; i < NUMBER_OF_TASK_RUNS_T2_BY_USER; i++) {
			WebDriverWait wait = new WebDriverWait(driver, 60000);
			wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//*[@id='TTImage']/div/div[1]")));
			
			WebElement image = driver.findElement(By
					.xpath("//*[@id='TTImage']/div/div[1]"));

			Actions builder = new Actions(driver);
			Action makeAnottation = builder.moveToElement(image).clickAndHold()
					.moveByOffset(100, 200).click().build();
			makeAnottation.perform();

			wait.until(ExpectedConditions.visibilityOfElementLocated(By
					.xpath("//*[@id='image-annotate-edit-form']/a[1]")));

			driver.findElement(
					By.xpath("//*[@id='image-annotate-edit-form']/a[1]"))
					.click();

			driver.findElement(By.xpath("//*[@id='button']")).click();
		}
	}

	@After
	public void tearDown() throws Exception {
		driver.quit();
		String verificationErrorString = verificationErrors.toString();
		if (!"".equals(verificationErrorString)) {
			fail(verificationErrorString);
		}
	}
}
