package regression;

public class LinearRegression {
	private Matrix theta, X, Y;
	/*
	 * Init Linear Regression
	 */
	public LinearRegression(double[][] X, double[][] Y){
		this.X = new Matrix(AddBias(X));
		this.Y = new Matrix(Y);
		int[] size = this.X.Size();
		this.theta = new Matrix(size[0],size[1]);
	}
	/*
	 * Add Bias
	 */
	public double[][] AddBias(double[][] data){
		int row = data.length, col = data[0].length;
		double[][] newdata = new double[row][col+1];
		for(int i = 0; i<row; i++){
			for(int j = 0; j<col; j++){
				if (j != 0){
					newdata[i][j] = data[i][j-1];
				}else{
					newdata[i][j] = 1.0;
				}
			}
		}
		return newdata;
	}
	/*
	 * Train Linear Regression
	 */
	public void Train(){
		
	}
}
