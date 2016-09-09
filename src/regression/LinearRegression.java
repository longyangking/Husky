package regression;

public class LinearRegression {
	private Matrix theta, X, Y;
	/*
	 * Init Linear Regression
	 */
	public LinearRegression(double[][] X, double[][] Y){
		this.X = new Matrix(X);
		this.Y = new Matrix(Y);
		int[] size = this.X.Size();
		this.theta = new Matrix(size[0],size[1]);
	}
	public LinearRegression(Matrix X, Matrix Y){
		this.X = X;
		this.Y = Y;
	}
	/*
	 * Train Linear Regression
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
