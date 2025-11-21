import React, { useState, useEffect } from 'react';
import { datasetAPI } from '../services/api';
import Header from './Header';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title, PointElement, LineElement } from 'chart.js';
import { Pie, Bar, Line, Scatter } from 'react-chartjs-2';
import { BoxPlotController, BoxAndWiskers } from '@sgratzl/chartjs-chart-boxplot';
import './Dashboard.css';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title, PointElement, LineElement, BoxPlotController, BoxAndWiskers);

const Dashboard = () => {
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [datasetDetail, setDatasetDetail] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Dynamic filter state
  const [selectedEquipmentType, setSelectedEquipmentType] = useState('all');
  const [selectedParameter, setSelectedParameter] = useState('flowrate');
  const [selectedChartType, setSelectedChartType] = useState('scatter');

  useEffect(() => {
    fetchDatasets();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchDatasets = async () => {
    try {
      const response = await datasetAPI.getAll();
      setDatasets(response.data);
      if (response.data.length > 0 && !selectedDataset) {
        loadDatasetDetail(response.data[0].id);
      }
    } catch (err) {
      setError('Failed to fetch datasets');
    }
  };

  const loadDatasetDetail = async (datasetId) => {
    try {
      const response = await datasetAPI.getDetail(datasetId);
      setDatasetDetail(response.data);
      setSelectedDataset(datasetId);
    } catch (err) {
      setError('Failed to load dataset details');
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      setError('Please upload a CSV file');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');

    try {
      await datasetAPI.upload(file);
      setSuccess('Dataset uploaded successfully!');
      fetchDatasets();
      e.target.value = '';
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload dataset');
    } finally {
      setUploading(false);
    }
  };

  const handleDownloadReport = async (datasetId) => {
    try {
      const response = await datasetAPI.downloadReport(datasetId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${datasetId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to generate report');
    }
  };

  const handleDeleteDataset = async (datasetId) => {
    if (!window.confirm('Are you sure you want to delete this dataset?')) return;

    try {
      await datasetAPI.delete(datasetId);
      setSuccess('Dataset deleted successfully');
      fetchDatasets();
      setDatasetDetail(null);
      setSelectedDataset(null);
    } catch (err) {
      setError('Failed to delete dataset');
    }
  };

  // Prepare chart data
  const getTypeDistributionChart = () => {
    if (!datasetDetail) return null;

    const distribution = datasetDetail.equipment_type_distribution;
    return {
      labels: Object.keys(distribution),
      datasets: [
        {
          label: 'Equipment Count',
          data: Object.values(distribution),
          backgroundColor: [
            '#0284c7',
            '#0891b2',
            '#14b8a6',
            '#10b981',
            '#84cc16',
            '#eab308',
          ],
          borderWidth: 1,
          borderColor: '#ffffff',
        },
      ],
    };
  };

  const getAveragesChart = () => {
    if (!datasetDetail) return null;

    return {
      labels: ['Flowrate', 'Pressure', 'Temperature'],
      datasets: [
        {
          label: 'Average Values',
          data: [
            datasetDetail.averages.flowrate,
            datasetDetail.averages.pressure,
            datasetDetail.averages.temperature,
          ],
          backgroundColor: ['#0284c7', '#14b8a6', '#84cc16'],
          borderWidth: 1,
          borderColor: '#e5e5e5',
        },
      ],
    };
  };

  const getFlowrateDistribution = () => {
    if (!datasetDetail) return null;
    const equipment = datasetDetail.equipment_details;
    const flowrates = equipment.map(e => parseFloat(e.flowrate)).sort((a, b) => a - b);
    const n = flowrates.length;
    
    const min = flowrates[0];
    const q1 = flowrates[Math.floor(n * 0.25)];
    const median = flowrates[Math.floor(n * 0.5)];
    const q3 = flowrates[Math.floor(n * 0.75)];
    const max = flowrates[n - 1];

    return {
      labels: ['Distribution'],
      datasets: [
        {
          label: `Min: ${min.toFixed(2)}`,
          data: [q1 - min],
          backgroundColor: '#0284c7',
          barThickness: 60,
        },
        {
          label: `Q1: ${q1.toFixed(2)}`,
          data: [median - q1],
          backgroundColor: '#0ea5e9',
          barThickness: 60,
        },
        {
          label: `Median: ${median.toFixed(2)}`,
          data: [q3 - median],
          backgroundColor: '#38bdf8',
          barThickness: 60,
        },
        {
          label: `Q3: ${q3.toFixed(2)}`,
          data: [max - q3],
          backgroundColor: '#7dd3fc',
          barThickness: 60,
        },
      ],
    };
  };

  const getPressureDistribution = () => {
    if (!datasetDetail) return null;
    const equipment = datasetDetail.equipment_details;
    const pressures = equipment.map(e => parseFloat(e.pressure)).sort((a, b) => a - b);
    const n = pressures.length;
    
    const min = pressures[0];
    const q1 = pressures[Math.floor(n * 0.25)];
    const median = pressures[Math.floor(n * 0.5)];
    const q3 = pressures[Math.floor(n * 0.75)];
    const max = pressures[n - 1];

    return {
      labels: ['Distribution'],
      datasets: [
        {
          label: `Min: ${min.toFixed(2)}`,
          data: [q1 - min],
          backgroundColor: '#14b8a6',
          barThickness: 60,
        },
        {
          label: `Q1: ${q1.toFixed(2)}`,
          data: [median - q1],
          backgroundColor: '#2dd4bf',
          barThickness: 60,
        },
        {
          label: `Median: ${median.toFixed(2)}`,
          data: [q3 - median],
          backgroundColor: '#5eead4',
          barThickness: 60,
        },
        {
          label: `Q3: ${q3.toFixed(2)}`,
          data: [max - q3],
          backgroundColor: '#99f6e4',
          barThickness: 60,
        },
      ],
    };
  };

  const getTemperatureDistribution = () => {
    if (!datasetDetail) return null;
    const equipment = datasetDetail.equipment_details;
    const temperatures = equipment.map(e => parseFloat(e.temperature)).sort((a, b) => a - b);
    const n = temperatures.length;
    
    const min = temperatures[0];
    const q1 = temperatures[Math.floor(n * 0.25)];
    const median = temperatures[Math.floor(n * 0.5)];
    const q3 = temperatures[Math.floor(n * 0.75)];
    const max = temperatures[n - 1];

    return {
      labels: ['Distribution'],
      datasets: [
        {
          label: `Min: ${min.toFixed(2)}`,
          data: [q1 - min],
          backgroundColor: '#84cc16',
          barThickness: 60,
        },
        {
          label: `Q1: ${q1.toFixed(2)}`,
          data: [median - q1],
          backgroundColor: '#a3e635',
          barThickness: 60,
        },
        {
          label: `Median: ${median.toFixed(2)}`,
          data: [q3 - median],
          backgroundColor: '#bef264',
          barThickness: 60,
        },
        {
          label: `Q3: ${q3.toFixed(2)}`,
          data: [max - q3],
          backgroundColor: '#d9f99d',
          barThickness: 60,
        },
      ],
    };
  };

  // Get available equipment types
  const getEquipmentTypes = () => {
    if (!datasetDetail) return [];
    return Object.keys(datasetDetail.equipment_type_distribution);
  };

  // Filter equipment data based on selected type
  const getFilteredEquipment = () => {
    if (!datasetDetail) return [];
    if (selectedEquipmentType === 'all') {
      return datasetDetail.equipment_details;
    }
    return datasetDetail.equipment_details.filter(
      eq => eq.equipment_type === selectedEquipmentType
    );
  };

  // Generate dynamic chart data
  const getDynamicChartData = () => {
    const filtered = getFilteredEquipment();
    if (filtered.length === 0) return null;

    const labels = filtered.map((_, idx) => `#${idx + 1}`);
    const parameterData = filtered.map(eq => parseFloat(eq[selectedParameter]));

    const colors = {
      flowrate: '#0284c7',
      pressure: '#14b8a6',
      temperature: '#84cc16',
    };

    if (selectedChartType === 'line') {
      return {
        labels,
        datasets: [
          {
            label: selectedParameter.charAt(0).toUpperCase() + selectedParameter.slice(1),
            data: parameterData,
            borderColor: colors[selectedParameter],
            backgroundColor: colors[selectedParameter] + '40',
            tension: 0.4,
            fill: true,
          },
        ],
      };
    } else if (selectedChartType === 'scatter') {
      return {
        datasets: [
          {
            label: selectedParameter.charAt(0).toUpperCase() + selectedParameter.slice(1),
            data: parameterData.map((value, idx) => ({ x: idx + 1, y: value })),
            backgroundColor: colors[selectedParameter],
            borderColor: colors[selectedParameter],
            pointRadius: 4,
          },
        ],
      };
    } else {
      // bar chart
      return {
        labels,
        datasets: [
          {
            label: selectedParameter.charAt(0).toUpperCase() + selectedParameter.slice(1),
            data: parameterData,
            backgroundColor: colors[selectedParameter],
            borderWidth: 1,
            borderColor: '#e5e5e5',
          },
        ],
      };
    }
  };

  return (
    <div className="dashboard">
      <Header showDashboardTitle={true} />

      <div className="dashboard-content">
        <aside className="sidebar">
          <div className="upload-section">
            <h3>Upload Dataset</h3>
            <label className="file-upload">
              <input
                type="file"
                accept=".csv"
                onChange={handleFileUpload}
                disabled={uploading}
              />
              {uploading ? 'Uploading...' : 'Choose CSV File'}
            </label>
          </div>

          <div className="datasets-list">
            <h3>My Datasets ({datasets.length}/5)</h3>
            {datasets.map((dataset) => (
              <div
                key={dataset.id}
                className={`dataset-item ${selectedDataset === dataset.id ? 'active' : ''}`}
                onClick={() => loadDatasetDetail(dataset.id)}
              >
                <div className="dataset-name">{dataset.filename}</div>
                <div className="dataset-date">
                  {new Date(dataset.uploaded_at).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        </aside>

        <main className="main-content">
          {error && <div className="alert alert-error">{error}</div>}
          {success && <div className="alert alert-success">{success}</div>}

          {datasetDetail ? (
            <>
              <div className="dataset-header">
                <h2>Dataset Analysis</h2>
                <div className="action-buttons">
                  <button
                    onClick={() => handleDownloadReport(selectedDataset)}
                    className="btn-action"
                  >
                    📄 Download Report
                  </button>
                  <button
                    onClick={() => handleDeleteDataset(selectedDataset)}
                    className="btn-danger"
                  >
                    🗑️ Delete
                  </button>
                </div>
              </div>

              <div className="stats-grid">
                <div className="stat-card">
                  <h3>Total Equipment</h3>
                  <p className="stat-value">{datasetDetail.total_count}</p>
                </div>
                <div className="stat-card">
                  <h3>Avg Flowrate</h3>
                  <p className="stat-value">{datasetDetail.averages.flowrate}</p>
                </div>
                <div className="stat-card">
                  <h3>Avg Pressure</h3>
                  <p className="stat-value">{datasetDetail.averages.pressure}</p>
                </div>
                <div className="stat-card">
                  <h3>Avg Temperature</h3>
                  <p className="stat-value">{datasetDetail.averages.temperature}</p>
                </div>
              </div>

              <div className="charts-grid">
                <div className="chart-card">
                  <h3>Equipment Type Distribution</h3>
                  <div className="chart-container">
                    <Pie data={getTypeDistributionChart()} />
                  </div>
                </div>
                <div className="chart-card">
                  <h3>Average Parameters</h3>
                  <div className="chart-container">
                    <Bar data={getAveragesChart()} />
                  </div>
                </div>
              </div>

              <div className="distribution-grid">
                <div className="chart-card">
                  <h3>Flowrate Distribution</h3>
                  <div className="chart-container">
                    <Bar 
                      data={getFlowrateDistribution()} 
                      options={{
                        indexAxis: 'y',
                        plugins: {
                          legend: {
                            display: true,
                            position: 'bottom',
                            labels: {
                              boxWidth: 12,
                              font: {
                                size: 11,
                              },
                            },
                          },
                        },
                        scales: {
                          x: {
                            stacked: true,
                            display: false,
                          },
                          y: {
                            stacked: true,
                            display: false,
                          },
                        },
                      }}
                    />
                  </div>
                </div>
                <div className="chart-card">
                  <h3>Pressure Distribution</h3>
                  <div className="chart-container">
                    <Bar 
                      data={getPressureDistribution()} 
                      options={{
                        indexAxis: 'y',
                        plugins: {
                          legend: {
                            display: true,
                            position: 'bottom',
                            labels: {
                              boxWidth: 12,
                              font: {
                                size: 11,
                              },
                            },
                          },
                        },
                        scales: {
                          x: {
                            stacked: true,
                            display: false,
                          },
                          y: {
                            stacked: true,
                            display: false,
                          },
                        },
                      }}
                    />
                  </div>
                </div>
                <div className="chart-card">
                  <h3>Temperature Distribution</h3>
                  <div className="chart-container">
                    <Bar 
                      data={getTemperatureDistribution()} 
                      options={{
                        indexAxis: 'y',
                        plugins: {
                          legend: {
                            display: true,
                            position: 'bottom',
                            labels: {
                              boxWidth: 12,
                              font: {
                                size: 11,
                              },
                            },
                          },
                        },
                        scales: {
                          x: {
                            stacked: true,
                            display: false,
                          },
                          y: {
                            stacked: true,
                            display: false,
                          },
                        },
                      }}
                    />
                  </div>
                </div>
              </div>

              <div className="chart-card">
                <h3>Dynamic Filterable Visualizer</h3>
                <div className="filter-controls">
                  <div className="filter-group">
                    <label>Equipment Type:</label>
                    <select 
                      value={selectedEquipmentType} 
                      onChange={(e) => setSelectedEquipmentType(e.target.value)}
                    >
                      <option value="all">All Types</option>
                      {getEquipmentTypes().map(type => (
                        <option key={type} value={type}>{type}</option>
                      ))}
                    </select>
                  </div>
                  <div className="filter-group">
                    <label>Parameter:</label>
                    <select 
                      value={selectedParameter} 
                      onChange={(e) => setSelectedParameter(e.target.value)}
                    >
                      <option value="flowrate">Flowrate</option>
                      <option value="pressure">Pressure</option>
                      <option value="temperature">Temperature</option>
                    </select>
                  </div>
                  <div className="filter-group">
                    <label>Chart Type:</label>
                    <select 
                      value={selectedChartType} 
                      onChange={(e) => setSelectedChartType(e.target.value)}
                    >
                      <option value="scatter">Scatter</option>
                      <option value="line">Line</option>
                      <option value="bar">Bar</option>
                    </select>
                  </div>
                </div>
                <div className="chart-container">
                  {selectedChartType === 'line' && <Line data={getDynamicChartData()} />}
                  {selectedChartType === 'scatter' && <Scatter data={getDynamicChartData()} />}
                  {selectedChartType === 'bar' && <Bar data={getDynamicChartData()} />}
                </div>
              </div>

              <div className="table-card">
                <h3>Equipment Details</h3>
                <div className="table-container">
                  <table>
                    <thead>
                      <tr>
                        <th>Equipment Name</th>
                        <th>Type</th>
                        <th>Flowrate</th>
                        <th>Pressure</th>
                        <th>Temperature</th>
                      </tr>
                    </thead>
                    <tbody>
                      {datasetDetail.equipment_details.map((eq, idx) => (
                        <tr key={idx}>
                          <td>{eq.equipment_name}</td>
                          <td>{eq.equipment_type}</td>
                          <td>{eq.flowrate}</td>
                          <td>{eq.pressure}</td>
                          <td>{eq.temperature}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          ) : (
            <div className="empty-state">
              <h2>No Dataset Selected</h2>
              <p>Upload a CSV file to get started</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
