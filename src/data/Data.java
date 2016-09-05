package data;

public class Data {
	private double[][] datas;
	public Data(double[][] datas){
		this.datas = datas;
	}
	public double[][] GetData(){
		return datas;
	}
	public static Data Add(Data data1, Data data2){
		double[][] datas1 = data1.GetData();
		double[][] datas2 = data2.GetData();
		return new Data(datas1);
	}
}
