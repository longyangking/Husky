package regression;

public class LogisticRegression {
	private Matrix theta, X, Y;
	public LogisticRegression(double[][] X, double[][] Y){
		this.X = new Matrix(X);
		this.Y = new Matrix(Y);
		int[] size = this.X.Size();
		this.theta = new Matrix(size[0],size[1]);
	}
	public LogisticRegression(Matrix X, Matrix Y){
		this.X = X;
		this.Y = Y;
	}
	/*
	 * Train Logistic Regression
	 */
	public void Train(){
		
	}
	/*
	 * Predict value
	 */
	public double Predict(double[] Xi){
		
	}
	public double Predict(Matrix Xi){
		
	}
}
