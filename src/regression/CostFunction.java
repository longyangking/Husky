package regression;

public class CostFunction {
	private Matrix X, Y;
	public CostFunction(Matrix X, Matrix Y){
		this.X = X; this.Y = Y;
	}
	public double LinearCost(Matrix theta){
		Matrix cost = Matrix.Sub(Matrix.Mul(theta, X), Y);
		cost = Matrix.Mul(Matrix.Transpose(cost), cost);
		int[] size = theta.Size(); int m = size[0];
		return cost.Sum()/m;
	}
	public double CrossEntropy(Matrix theta){
		int[] size = theta.Size(); int m = size[0];
		Matrix H = Matrix.Mul(theta, X) ;
		double[][] Hs = H.GetData(), Ys = Y.GetData();
		int row = Hs.length, col = Hs[0].length;
		double sum = 0, h = 0, y = 0;
		for(int i = 0; i<row; i++){
			h = Preprocess.Sigmoid(Hs[i][0]);
			y = Ys[i][0];
			sum += -y*Math.log(h)-(1-y)*Math.log(1-h);
		}
		return sum/m;
	}
}
