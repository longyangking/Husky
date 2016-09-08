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
		
	}
}
