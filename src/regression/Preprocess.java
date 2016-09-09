package regression;

public class Preprocess {
	public static double[] MeanNorm(double[] data){
		double mu = 0, sigma = 0, sum = 0;
		for(int i = 0; i<data.length; i++){
			sum += data[i];
		}
		mu = sum/data.length; 
		sum = 0;
		for(int i = 0; i<data.length; i++){
			sum += Math.pow(data[i]-mu, 2);
		}
		sigma = Math.sqrt(sum/data.length);
		if (sigma == 0){
			sigma = 1; //No Variance, but keep the form of following mean normalization
		}
		for(int i = 0; i<data.length; i++){
			data[i] = (data[i]-mu)/sigma;
		}
		return data;
	}
	/*
	 * Add Bias
	 */
	public static double[][] AddBias(double[][] data){
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
	 * Sigmoid Function
	 */
	public static double Sigmoid(double value){
		return 1.0/(1.0+Math.exp(value));
	}
}
