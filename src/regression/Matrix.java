package regression;
import java.util.Arrays;
/*
 * Temporary Implementation (will be replaced in the future)
 */
public class Matrix {
	private double[][] data;
	/*
	 * Init Matrix with all Zero
	 */
	public Matrix(int row, int col){
		data = new double[row][col];
	}
	/*
	 * Init Matrix by Data
	 */
	public Matrix(double[][] data){
		this.data = data;
	}
	public int[] Size(){
		int row = data.length, col = data[0].length;
		return new int[]{row,col};
	}
	public double[][] GetData(){
		return this.data;
	}
	public void SetData(int row, int col, double value){
		this.data[row][col] = value;
	}
	public Matrix Clone(){
		return new Matrix(this.data);
	}
	/*
	 * Matrix Add
	 */
	public static Matrix Add(Matrix A, Matrix B){
		int[] sizeA = A.Size(), sizeB = B.Size();
		if (!Arrays.equals(sizeA, sizeB)) {
			new Exception("Matrix Add: Dimension not match!");
		}
		int row = sizeA[0], col = sizeA[1];
		double[][] newdata = new double[row][col], dataA = A.GetData(), dataB = B.GetData();
		for(int i = 0; i<row; i++){
			for(int j = 0; j<col; j++){
				newdata[i][j] = dataA[i][j] + dataB[i][j];
			}
		}
		return new Matrix(newdata);
	}
	/*
	 * Matrix Sub
	 */
	public static Matrix Sub(Matrix A, Matrix B){
		int[] sizeA = A.Size(), sizeB = B.Size();
		if (!Arrays.equals(sizeA, sizeB)) {
			new Exception("Matrix Sub: Dimension not match!");
		}
		int row = sizeA[0], col = sizeA[1];
		double[][] newdata = new double[row][col], dataA = A.GetData(), dataB = B.GetData();
		for(int i = 0; i<row; i++){
			for(int j = 0; j<col; j++){
				newdata[i][j] = dataA[i][j] - dataB[i][j];
			}
		}
		return new Matrix(newdata);
	}
	/*
	 * Matrix Multiplication
	 */
	public static Matrix Mul(Matrix A, Matrix B){
		int[] sizeA = A.Size(), sizeB = B.Size();
		if (sizeA[1] != sizeB[0]) {
			new Exception("Matrix Mul: Dimension not match!");
		}
		int row = sizeA[0], col = sizeB[1], all = sizeA[1];
		double[][] newdata = new double[row][col], dataA = A.GetData(), dataB = B.GetData();
		for(int i = 0; i<row; i++){
			for(int j = 0; j<col; j++){
				double sum = 0;
				for(int k = 0; k < all; k++){
					sum += dataA[i][k]*dataB[k][j];
				}
				newdata[i][j] = sum;
			}
		}
		return new Matrix(newdata);
	}
	/*
	 * Matrix Tranpose
	 */
	public static Matrix Transpose(Matrix matrix){
		int[] size = matrix.Size();
		int row = size[0], col = size[1];
		double[][] data = matrix.GetData(), newdata = new double[col][row];
		for(int i = 0; i<row; i++){
			for(int j = 0; j<col; j++){
				newdata[j][i] = data[i][j];
			}
		}
		return new Matrix(newdata);
	}
}
