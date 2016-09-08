package regression;

public class MeanNormalization {
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
}
