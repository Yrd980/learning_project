package com.ruoyi.entertainment.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.entertainment.mapper.PerformancegroupsMapper;
import com.ruoyi.entertainment.domain.Performancegroups;
import com.ruoyi.entertainment.service.IPerformancegroupsService;

/**
 * 演出团体信息Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-08
 */
@Service
public class PerformancegroupsServiceImpl implements IPerformancegroupsService 
{
    @Autowired
    private PerformancegroupsMapper performancegroupsMapper;

    /**
     * 查询演出团体信息
     * 
     * @param id 演出团体信息主键
     * @return 演出团体信息
     */
    @Override
    public Performancegroups selectPerformancegroupsById(Long id)
    {
        return performancegroupsMapper.selectPerformancegroupsById(id);
    }

    /**
     * 查询演出团体信息列表
     * 
     * @param performancegroups 演出团体信息
     * @return 演出团体信息
     */
    @Override
    public List<Performancegroups> selectPerformancegroupsList(Performancegroups performancegroups)
    {
        return performancegroupsMapper.selectPerformancegroupsList(performancegroups);
    }

    /**
     * 新增演出团体信息
     * 
     * @param performancegroups 演出团体信息
     * @return 结果
     */
    @Override
    public int insertPerformancegroups(Performancegroups performancegroups)
    {
        return performancegroupsMapper.insertPerformancegroups(performancegroups);
    }

    /**
     * 修改演出团体信息
     * 
     * @param performancegroups 演出团体信息
     * @return 结果
     */
    @Override
    public int updatePerformancegroups(Performancegroups performancegroups)
    {
        return performancegroupsMapper.updatePerformancegroups(performancegroups);
    }

    /**
     * 批量删除演出团体信息
     * 
     * @param ids 需要删除的演出团体信息主键
     * @return 结果
     */
    @Override
    public int deletePerformancegroupsByIds(Long[] ids)
    {
        return performancegroupsMapper.deletePerformancegroupsByIds(ids);
    }

    /**
     * 删除演出团体信息信息
     * 
     * @param id 演出团体信息主键
     * @return 结果
     */
    @Override
    public int deletePerformancegroupsById(Long id)
    {
        return performancegroupsMapper.deletePerformancegroupsById(id);
    }
}
